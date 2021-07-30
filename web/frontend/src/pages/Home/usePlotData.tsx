import { useMutation } from "react-query";

export default function usePlotData() {
    return useMutation('getPlotData', (newRequest) => fetch('/api/recommend_routes', {
        method: 'post',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(newRequest)
    }).then(function(response) {
        return response.json();
    }));
}
