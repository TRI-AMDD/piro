import { FC } from 'react';
import Amplify from 'aws-amplify';
import { AmplifyAuthenticator, AmplifySignIn, AmplifySignUp } from '@aws-amplify/ui-react';

Amplify.configure(AWS_CONFIG);

const AmplifySetup: FC = ({ children }) => {
    if (!AMPLIFY_ENABLED) {
        return <>{children}</>;
    }

    return (        
        <AmplifyAuthenticator usernameAlias="email">
            <AmplifySignIn
                headerText="Sign In To Synthesis Analyzer"
                slot="sign-in"
            />
            <AmplifySignUp
                headerText="Sign Up for Synthesis Analyzer"
                slot="sign-up"
                usernameAlias="email"
                formFields={[
                    {
                        type: "email",
                        label: "Email",
                        placeholder: "Email",
                        inputProps: { required: true, autocomplete: "email" },
                    },
                    {
                        type: "password",
                        label: "Password",
                        placeholder: "Password",
                        inputProps: { required: true, autocomplete: "new-password" },
                    }
                ]}
            />
            {children}
        </AmplifyAuthenticator>
    );

};

export default AmplifySetup;
