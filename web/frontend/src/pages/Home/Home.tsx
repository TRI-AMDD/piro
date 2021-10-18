import { Auth } from 'aws-amplify';
import { useEffect, useState } from 'react';
import Form from './Form';
import SynthesisPlot from './SynthesisPlot';
import { PlotDataProvider } from './plotDataContext';

function Home() {
    const [token, setToken] = useState('');

    useEffect(() => {
        async function fetchToken() {
            const awsToken = `${(await Auth.currentSession()).getIdToken().getJwtToken()}`;
            console.log(awsToken);
            setToken(awsToken);
        }

        fetchToken();
    }, []);

    return (
        <PlotDataProvider token={token}>
            <Form />
            <SynthesisPlot />
        </PlotDataProvider>
    );
}

export default Home;
