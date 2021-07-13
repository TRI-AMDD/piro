import styled from '@emotion/styled';
import CounterPage from './Counter';
import Cats from './Cats';

const StyledCats = styled(Cats)`
    font-size: 1.2rem;
    list-style-type: circle;
    list-style-position: inside;
`;

function Demo() {
    return (
        <div>
            <CounterPage />
            <StyledCats />
        </div>
    );
}

export default Demo;
