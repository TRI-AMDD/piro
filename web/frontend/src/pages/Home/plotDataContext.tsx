import { FC, createContext, useContext, useState, useMemo, useEffect } from 'react';
import { UseMutationResult } from 'react-query';
import { Auth, Hub } from 'aws-amplify';
import { useSubmitTask, useNormalPlotData } from './usePlotData';

type ContextProps = {
    apiMode: string;
    token: string;
    setApiMode: (v: string) => void;
    mutation: UseMutationResult<any, unknown, void, unknown>;
};

const PlotDataContext = createContext({} as ContextProps);

const PlotDataProvider: FC = ({ children }) => {
    const [apiMode, setApiMode] = useState('task');
    const [token, setToken] = useState('');

    // fetch the token to be used for api calls when user has signed in or up
    useEffect(() => {
        Hub.listen('auth', (data) => {
            const event = data.payload.event;
            if (event === 'signIn' || event === 'signUp') {
                Auth.currentSession()
                    .then((session) => { setToken(session.getIdToken().getJwtToken()) })
                    .catch(() => {})
            }
        })

        Auth.currentSession()
            .then((session) => { setToken(session.getIdToken().getJwtToken()) })
            .catch(() => {})
    }, []);

    const taskMutation = useSubmitTask(token);
    const normalMutation = useNormalPlotData(token);

    const value = useMemo(() => ({
        apiMode,
        setApiMode,
        token,
        mutation: apiMode === 'task' ? taskMutation : normalMutation,
    }), [apiMode, taskMutation, normalMutation, token]);
    return <PlotDataContext.Provider value={value}>{children}</PlotDataContext.Provider>;
};

function usePlotData() {
    const context = useContext(PlotDataContext);
    if (context === undefined) {
        throw new Error('useApiModeContext must be used within a ApiModeProvider');
    }
    return context;
}

export { PlotDataProvider, usePlotData };
