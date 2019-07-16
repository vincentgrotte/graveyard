import { Component, OnDestroy, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { faCircle } from '@fortawesome/free-solid-svg-icons';
import { Subscription } from 'rxjs';
import { finalize } from 'rxjs/operators';
import { LocalStorageService } from '../../helpers/local-storage.helper';
import { AuthModel } from '../../models/auth.model';
import { LoginModel } from '../../models/login.model';
import { AuthService } from '../../services/auth.service';
import { NavigationService } from '../../services/core/navigation.service';
import { DateService } from '../../services/date.service';
import { IdleRedirectService } from '../../services/idle-redirect.service';
import { ModalService } from '../../services/modal.service';
import { TimeoutService } from '../../services/timeout.service';
import { DEVMODE_CONSTANTS } from './devmode.constants';

@Component({
  selector: 'app-devmode',
  templateUrl: './devmode.component.html',
  styleUrls: ['./devmode.component.scss']
})
export class DevModeComponent implements OnInit, OnDestroy {
    public IDLE_PAUSED: string = 'IDLE-PAUSED';
    public activeTimer: number = 0;
    public currentUser = undefined;
    public faCircle = faCircle;
    public IDLE_ON: string = 'IDLE-ON';
    public idleTimer: number = 0;
    public isIdleRedirectON: boolean = false;
    public users = DEVMODE_CONSTANTS.USERS;

    private subscriptions: Subscription = new Subscription();

  constructor(private activatedRoute: ActivatedRoute,
              private authService: AuthService,
              private dateService: DateService,
              private idleRedirectService: IdleRedirectService,
              private localStorageService: LocalStorageService,
              private modalService: ModalService,
              private navigationService: NavigationService,
              private router: Router,
              private timeoutService: TimeoutService
        ) {}

  public ngOnInit(): void {
        const getUser = this.authService.getUser();
        if (getUser) { this.currentUser = getUser.user; }
        this.subscriptions.add(this.timeoutService.getSecondInterval().subscribe(() => {
            if (this.idleRedirectService.isRunning) {
                this.activeTimer = 0;
                this.idleTimer++;
                this.isIdleRedirectON = true;
            } else {
                this.activeTimer++;
                this.idleTimer = 0;
                this.isIdleRedirectON = false;
            }
        }));
    }

    public ngOnDestroy(): void {
        this.subscriptions.unsubscribe();
    }

  public logout(): void {
    this.authService.clearStoragesAndReturnToLogin();
  }

    public toggleIdleRedirect(): void {
        if (this.idleRedirectService.isRunning) {
            this.idleRedirectService.stop();
        } else {
            this.idleRedirectService.start();
        }
    }

    public setUser(user): void {
        const returnRoute = this.activatedRoute.snapshot.queryParams['return']
            ? this.activatedRoute.snapshot.queryParams['return']
            : '/';
        const authForm = new LoginModel();
        authForm.createForm();
        authForm.email = user.email;
        authForm.password = user.pass;
        const submitSubscription = this.authService.postLogin(authForm)
                .pipe(finalize(() => submitSubscription.unsubscribe()))
                .subscribe((loginData: AuthModel) => {
                    this.authService.saveToken(loginData, authForm.remember);
                    window.location.reload();
                    this.navigationService.setRoute([returnRoute]);
                });
    }

}
