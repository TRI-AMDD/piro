var AWS_CONFIG = {
    Auth: {

        // REQUIRED only for Federated Authentication - Amazon Cognito Identity Pool ID
        // identityPoolId: 'XX-XXXX-X:XXXXXXXX-XXXX-1234-abcd-1234567890ab',

        // REQUIRED - Amazon Cognito Region
        region: 'FILL_IN',

        // OPTIONAL - Amazon Cognito User Pool ID
        userPoolId: 'FILL_IN',

        // OPTIONAL - Amazon Cognito Web Client ID (26-char alphanumeric string)
        userPoolWebClientId: 'FILL_IN',

        // OPTIONAL - Enforce user authentication prior to accessing AWS resources or not
        mandatorySignIn: false,
        /*
        // OPTIONAL - Configuration for cookie storage
        // Note: if the secure flag is set to true, then the cookie transmission requires a secure protocol
        cookieStorage: {
            // REQUIRED - Cookie domain (only required if cookieStorage is provided)
            domain: '.yourdomain.com',
            // OPTIONAL - Cookie path
            path: '/',
            // OPTIONAL - Cookie expiration in days
            expires: 365,
            // OPTIONAL - See: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Set-Cookie/SameSite
            sameSite: 'lax',
            // OPTIONAL - Cookie secure flag
            // Either true or false, indicating if the cookie transmission requires a secure protocol (https).
            secure: true
        },

        // OPTIONAL - Manually set the authentication flow type. Default is 'USER_SRP_AUTH'
        authenticationFlowType: 'USER_PASSWORD_AUTH',

        // OPTIONAL - Manually set key value pairs that can be passed to Cognito Lambda Triggers
        clientMetadata: { myCustomKey: 'myCustomValue' },

        // OPTIONAL - Hosted UI configuration
        oauth: {
            domain: 'your_cognito_domain',
            scope: ['phone', 'email', 'profile', 'openid', 'aws.cognito.signin.user.admin'],
            redirectSignIn: 'http://localhost:3000/',
            redirectSignOut: 'http://localhost:3000/',
            responseType: 'code' // or 'token', note that REFRESH token will only be generated when the responseType is code
        }
        */
    }
};
// base url prepend for all api calls
var API_BASE_URL = "";

// boolean flag to set amplify on/off for user authentication support
var AMPLIFY_ENABLED = true;