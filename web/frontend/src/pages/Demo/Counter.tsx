import { Button } from '@toyota-research-institute/lakefront';
import styled from '@emotion/styled';
import { useCounter, CounterProvider } from 'contexts/countContext';

const Count = styled.span`
    display: inline-block;
    font-size: 1.2rem;
    margin: 0 4px;
`;

const Counter = () => {
    const { count, handleIncrement, handleDecrement } = useCounter();

    return (
        <p>
            <Button type="button" color="destructive" onClick={handleDecrement}>
                Decrement
            </Button>
            <Count>Count: {count}</Count>
            <Button type="button" onClick={handleIncrement}>
                Increment
            </Button>
        </p>
    );
};

function CounterPage() {
    return (
        <div className="App">
            <CounterProvider>
                <Counter />
            </CounterProvider>
        </div>
    );
}

export default CounterPage;
