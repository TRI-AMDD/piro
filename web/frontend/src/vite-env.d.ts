/// <reference types="vite/client" />
declare const AWS_CONFIG: {
  Auth: {
    region: string;
    userPoolId: string;
    userPoolWebClientId: string;
    mandatorySignIn: boolean;
  };
};
declare const API_BASE_URL: string;
declare const AMPLIFY_ENABLED: boolean;
declare const dataLayer: Record<string, string>[];
