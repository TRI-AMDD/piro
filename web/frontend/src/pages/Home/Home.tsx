import Form from './Form';
import SynthesisPlot from './SynthesisPlot';
import { PlotDataProvider } from './plotDataContext';
import styles from './Home.module.css';

function Home() {
  return (
    <div className={styles.appBody}>
      <PlotDataProvider>
        <Form />
        <SynthesisPlot />
      </PlotDataProvider>
    </div>
  );
}

export const element = <Home />;

export default Home;
