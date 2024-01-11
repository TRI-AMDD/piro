import Plot from 'react-plotly.js';
import styles from './Home.module.css';

interface Props {
  result: {
    data: Plotly.Data[];
    layout: Partial<Plotly.Layout>;
  };
}

function PlotResults(props: Props) {
  const { result } = props;

  return (
    <div className={styles.Plot}>
      <Plot {...result} />
    </div>
  );
}

export default PlotResults;
