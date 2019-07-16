const users = [
    { rank: 8, write: true, name: 'Admin', email: 'vince+admin@inthecode.com.au', pass: 'qwerty' },
    { rank: 7, write: true, name: 'Corporate/master', email: 'vince+master@inthecode.com.au', pass: 'qwerty' },
    { rank: 6, write: false, name: 'Corporate/read-write', email: 'vince+readWrite@inthecode.com.au', pass: 'qwerty' },
    { rank: 5, write: true, name: 'Corporate/read-only', email: 'vince+readOnly@inthecode.com.au', pass: 'qwerty' },
    { rank: 4, write: true, name: 'Area Manager', email: 'vince+area@inthecode.com.au', pass: 'qwerty' },
    { rank: 3, write: true, name: 'Store/Franchisee', email: 'vince+franchisee@inthecode.com.au', pass: 'qwerty' },
    { rank: 2, write: true, name: 'Store/Manager', email: 'vince+storemanager@inthecode.com.au', pass: 'qwerty' },
    { rank: 1, write: false, name: 'Store', email: 'vince+store@inthecode.com.au', pass: 'qwerty' }
];

export const DEVMODE_CONSTANTS = {
    USERS: users
};
