import { useMutation, useQuery } from "react-query";

export const useSubmitTask = (token: string) => {
    return useMutation('submitTask', (newRequest) => fetch('/api/recommend_routes_task', {
        method: 'post',
        headers: {
            'Content-Type': 'application/json',
            'Accept-Encoding': 'gzip',
            Authorization: `Bearer ${token}`
        },
        body: JSON.stringify(newRequest)
    }).then(function(response) {
        return response.json();
    }));
}

export const useNormalPlotData = (token: string) => {
    return useMutation('submitRoute', (newRequest) => fetch('/api/recommend_routes', {
        method: 'post',
        headers: {
            'Content-Type': 'application/json',
            'Accept-Encoding': 'gzip',
            Authorization: `Bearer ${token}`
        },
        body: JSON.stringify(newRequest)
    }).then(function(response) {
        return response.json();
    }));
}

export const useTaskPlotData = (taskId: string, token: string) => {
    return useQuery(
        ["getPlotData", taskId],
        async () => {
            const response = await fetch(`/api/recommend_routes_task/${taskId}`, {
                headers: {
                    'Accept-Encoding': 'gzip',
                    Authorization: `Bearer ${token}`
                },
            });
            const data = await response.json();
            // throw an error if status is started to trigger loading
            if (data?.status === 'started' || data?.status === 'pending') {
                throw new Error("Request initiated. Loading Results...");
            }
            return data
        },
        {
            enabled: !!taskId,
            refetchOnWindowFocus: false,
            retry: true
        }
    );
}
