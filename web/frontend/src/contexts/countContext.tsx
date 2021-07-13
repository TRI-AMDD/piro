import React, { FC, createContext, useContext, useState, useMemo } from 'react';

const CounterContext = createContext(
    {} as {
        count: number;
        handleIncrement: () => void;
        handleDecrement: () => void;
    }
);

const CounterProvider: FC = ({ children }) => {
    const [count, setCount] = useState(0);

    const handleIncrement = () => {
        setCount((prevCount) => prevCount + 1);
    };

    const handleDecrement = () => {
        setCount((prevCount) => Math.max(0, prevCount - 1));
    };

    const value = useMemo(() => ({ count, handleIncrement, handleDecrement }), [count]);
    return <CounterContext.Provider value={value}>{children}</CounterContext.Provider>;
};

function useCounter() {
    const context = useContext(CounterContext);
    if (context === undefined) {
        throw new Error('useCounterContext must be used within a CounterProvider');
    }
    return context;
}

export { CounterProvider, useCounter };
