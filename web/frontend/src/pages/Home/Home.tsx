import Form from './Form';
import SynthesisPlot from "./SynthesisPlot";
import { ApiModeProvider } from './apiModeContext';

function Home() {
    return (
        <ApiModeProvider>
            <Form />
            <SynthesisPlot />
        </ApiModeProvider>
    );
}

export default Home;
