import Form from './Form';
import SynthesisPlot from './SynthesisPlot';
import { PlotDataProvider } from './plotDataContext';

function Home() {
  return (
    <PlotDataProvider>
      <Form />
      <SynthesisPlot />
    </PlotDataProvider>
  );
}

export default Home;
