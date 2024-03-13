import { useQuery, useMutation } from '@tanstack/react-query';
import { Inputs, Results } from './TypeProps';

export const useSubmitTask = (token: string) => {
  return useMutation({
    mutationFn: (newRequest: Inputs): Promise<Results> => {
      return fetch(`${API_BASE_URL}/api/recommend_routes_task`, {
        method: 'post',
        headers: {
          'Content-Type': 'application/json',
          'Accept-Encoding': 'gzip',
          Authorization: `Bearer ${token}`
        },
        body: JSON.stringify(newRequest)
      }).then(function (response) {
        return response.json();
      });
    }
  });
};

export const useNormalPlotData = (token: string) => {
  return useMutation({
    mutationFn: (newRequest: Inputs): Promise<Results> => {
      return fetch(`${API_BASE_URL}/api/recommend_routes`, {
        method: 'post',
        headers: {
          'Content-Type': 'application/json',
          'Accept-Encoding': 'gzip',
          Authorization: `Bearer ${token}`
        },
        body: JSON.stringify(newRequest)
      }).then(function (response) {
        return response.json();
      });
    }
  });
};

export const useTaskPlotData = (taskId: string, token: string) => {
  return useQuery({
    queryKey: ['getPlotData'],
    queryFn: async (): Promise<Results> => {
      const response = await fetch(`${API_BASE_URL}/api/recommend_routes_task/${taskId}`, {
        headers: {
          'Accept-Encoding': 'gzip',
          Authorization: `Bearer ${token}`
        }
      });
      const data = await response.json();
      return data;
    },
    enabled: !!taskId,
    refetchInterval: query => {      
      if (query.state.data) {
        const { status } = query.state.data;
        // re-fetch results in 2 secs if status is pending
        if (status === 'started' || status === 'pending') {
          return 2000;
        }        
      }
      
      return false;
    },
    refetchOnWindowFocus: false,
    retry: true
  });
};
