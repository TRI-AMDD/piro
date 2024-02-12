import { Loading } from '@toyota-research-institute/lakefront';
import { useTaskPlotData } from './usePlotData';
import styles from './Home.module.css';
import ErrorMessage from './ErrorMessage';
import PlotResults from './PlotResults';
import { usePlotData } from './plotDataContext';
import { pushEvent } from 'src/utils/GA';

interface Props {
  taskId: string;
}

function TaskPlot(props: Props) {
  const { taskId } = props;
  const { token } = usePlotData();
  const { data, error, isLoading } = useTaskPlotData(taskId, token);

  if (isLoading)
    return (
      <div className={styles.Loading}>
        <Loading animated height={24} label="Loading..." width={24} />
      </div>
    );

  if (error) {
    pushEvent("Error encountered")
    return <ErrorMessage error="Error encountered" />;
  }

  if (!data) {
    return null;
  }

  if (data.status === 'started' || data.status === 'pending') {
    return (
      <div className={styles.Loading}>
        <Loading animated height={24} label="Request initiated. Loading Results..." width={24} />
      </div>
    );
  }

  if (data.status === 'failure') {
    pushEvent("Failure")
    return <ErrorMessage error={data.error_message} />;
  }

  if (data.status === 'invalid') {
    pushEvent("Invalid request sent")
    return <ErrorMessage error="Invalid request sent." />;
  }

  return <PlotResults result={data.result} />;
}

export default TaskPlot;
