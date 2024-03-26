import Plot from 'react-plotly.js';
import styles from './Home.module.css';
import { pushEvent } from 'src/utils/GA';
import { useEffect, useRef } from 'react';

interface Props {
  result: {
    data: Plotly.Data[];
    layout: Partial<Plotly.Layout>;
  };
}

const handleDivLoad = () => {
  pushEvent('plot successfully rendered');
};

function PlotResults(props: Props) {
  const { result } = props;
  const plotDivRef = useRef<HTMLDivElement>(null);
  useEffect(() => {
    window.scrollTo(0, document.body.scrollHeight);
  }, []);
  useEffect(() => {
    const plotDiv = plotDivRef.current;

    if (plotDiv) {
      plotDiv.addEventListener('load', handleDivLoad);

      return () => {
        plotDiv.removeEventListener('load', handleDivLoad);
      };
    }
  }, []);

  return (
    <div className={styles.Plot} ref={plotDivRef}>
      <Plot {...result} />
    </div>
  );
}

export default PlotResults;
