import { TRIAppConfig } from '@toyotaresearchinstitute/rse-react-library';

export default {
  name: 'Piro Synthesis Analyzer',
  AWSConfig: {
    Auth: {
      // REQUIRED only for Federated Authentication - Amazon Cognito Identity Pool ID
      // identityPoolId: 'XX-XXXX-X:XXXXXXXX-XXXX-1234-abcd-1234567890ab',

      // REQUIRED - Amazon Cognito Region
      region: 'us-east-1',

      // OPTIONAL - Amazon Cognito User Pool ID
      userPoolId: 'us-east-1_szOwM3jV5',

      // OPTIONAL - Amazon Cognito Web Client ID (26-char alphanumeric string)
      userPoolWebClientId: 'ejvbd73d50i0j01jcmt9s3o7j',

      // OPTIONAL - Enforce user authentication prior to accessing AWS resources or not
      mandatorySignIn: true,

      // OPTIONAL - This is used when autoSignIn is enabled for Auth.signUp
      // 'code' is used for Auth.confirmSignUp, 'link' is used for email link verification
      signUpVerificationMethod: 'code',
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
          */
      oauth: {
        domain: 'prod-synthesis-app.auth.us-east-1.amazoncognito.com',
        scope: ['email', 'openid'],
        redirectSignIn: 'https://piro.matr.io',
        redirectSignOut: 'https://piro.matr.io',
        responseType: 'code' // or 'token', note that REFRESH token will only be generated when the responseType is code
      }
    }
  },
  // base url prepend for all api calls
  apiBaseUrl: window.location.origin,
  // boolean flag to set amplify on/off for user authentication support
  amplifyEnabled: true,
  // OPTIONAL: URL to post feedback to JIRA
  issueCollectorUrl:
    'https://toyotaresearchinstitute.atlassian.net/s/d41d8cd98f00b204e9800998ecf8427e-T/tod1zk/b/5/c95134bc67d3a521bb3f4331beb9b804/_/download/batch/com.atlassian.jira.collector.plugin.jira-issue-collector-plugin:issuecollector/com.atlassian.jira.collector.plugin.jira-issue-collector-plugin:issuecollector.js?locale=en-US&collectorId=784fa038'
} as TRIAppConfig;
