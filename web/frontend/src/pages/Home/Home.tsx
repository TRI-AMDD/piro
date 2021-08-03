import Form from './Form';
import SynthesisPlot from "./SynthesisPlot";
import { useSubmitTask } from "./usePlotData";

function Home() {
    const mutation = useSubmitTask();

    return (
        <>
            <Form mutation={mutation} />
            <SynthesisPlot mutation={mutation} />
        </>
    );
}

export default Home;
