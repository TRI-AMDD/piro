import Plot from 'react-plotly.js';
import { useQuery } from "react-query";
import styles from './Home.module.css';

interface Props {
    request: any;
}

function SynthesisPlot(props: Props) {
    const { request } = props;
    const { data, error, isLoading } = useQuery('plotData', () => fetch('/api/recommend_routes', {
        method: 'post',
        body: JSON.stringify(request)
    }).then(function(response) {
        return response.json();
    }));

    if (isLoading) return <>Loading...</>;

    if (error) {
        return <>An error has occurred</>;
    }

    console.log(request);
    console.log(data);

    return (
        <div className={styles.Plot}>
            <Plot {...data} />
        </div>
    );
}

export default SynthesisPlot;
