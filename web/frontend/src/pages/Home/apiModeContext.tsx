import React, { FC, createContext, useContext, useState, useMemo } from 'react';
import { useSubmitTask, useNormalPlotData } from './usePlotData';
import { UseMutationResult } from 'react-query';

type ContextProps = {
    apiMode: string;
    setApiMode: (v: string) => void;
    mutation: UseMutationResult<any, unknown, void, unknown>;
};

const ApiModeContext = createContext({} as ContextProps);

const ApiModeProvider: FC = ({ children }) => {
    const [apiMode, setApiMode] = useState('task');
    const taskMutation = useSubmitTask();
    const normalMutation = useNormalPlotData();

    const value = useMemo(() => ({
        apiMode,
        setApiMode,
        mutation: apiMode === 'task' ? taskMutation : normalMutation
    }), [apiMode, taskMutation, normalMutation]);
    return <ApiModeContext.Provider value={value}>{children}</ApiModeContext.Provider>;
};

function useApiMode() {
    const context = useContext(ApiModeContext);
    if (context === undefined) {
        throw new Error('useApiModeContext must be used within a ApiModeProvider');
    }
    return context;
}

export { ApiModeProvider, useApiMode };
