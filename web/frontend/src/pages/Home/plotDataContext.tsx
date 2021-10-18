import React, { FC, createContext, useContext, useState, useMemo } from 'react';
import { useSubmitTask, useNormalPlotData } from './usePlotData';
import { UseMutationResult } from 'react-query';

type ContextProps = {
    apiMode: string;
    token: string;
    setApiMode: (v: string) => void;
    mutation: UseMutationResult<any, unknown, void, unknown>;
};

const PlotDataContext = createContext({} as ContextProps);

interface Props {
    token: string
}

const PlotDataProvider: FC<Props> = ({ token, children }) => {
    const [apiMode, setApiMode] = useState('task');
    const taskMutation = useSubmitTask(token);
    const normalMutation = useNormalPlotData(token);

    const value = useMemo(() => ({
        apiMode,
        setApiMode,
        token,
        mutation: apiMode === 'task' ? taskMutation : normalMutation
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
