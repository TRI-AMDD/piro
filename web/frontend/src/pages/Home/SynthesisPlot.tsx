import { Loading } from '@toyota-research-institute/lakefront';
import styles from './Home.module.css';
import ErrorMessage from './ErrorMessage';
import PlotResults from './PlotResults';
import { usePlotData } from './plotDataContext';
import TaskPlot from './TaskPlot';

function SynthesisPlot() {
  const { mutation, apiMode } = usePlotData();
  const { data, error, isLoading } = mutation;

  if (isLoading)
    return (
      <div className={styles.Loading}>
        <Loading animated height={24} label="Loading..." width={24} />
      </div>
    );

  if (error) {
    return <ErrorMessage error="An error has occurred when making the api call." />;
  }

  if (!data) {
    return null;
  }

  if (data.detail) {
    return <ErrorMessage error={data.detail} />;
  }

  if (data.error_message) {
    return <ErrorMessage error={data.error_message} />;
  }

  if (apiMode === 'task') {
    return <TaskPlot key={data.task_id} taskId={data.task_id} />;
  }

  return <PlotResults result={data} />;
}

export default SynthesisPlot;
