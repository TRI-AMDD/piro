import { FC } from 'react';
import { QueryClient, QueryClientProvider } from 'react-query';

const queryClient = new QueryClient();

export const MockQuery: FC = (props) => {
    const { children } = props;

    return <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>;
};

export default MockQuery;
