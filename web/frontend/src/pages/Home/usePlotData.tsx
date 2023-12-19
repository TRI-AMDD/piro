import { useQuery, useMutation } from '@tanstack/react-query';
import { useUserAuth } from '@/features/cognito/use-user-auth';

export const useSubmitTask = (token: string) => {
  return useMutation({
    mutationFn: (newRequest) => {
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
  /*
  return useMutation('submitTask', (newRequest) =>
    fetch(`${API_BASE_URL}/api/recommend_routes_task`, {
      method: 'post',
      headers: {
        'Content-Type': 'application/json',
        'Accept-Encoding': 'gzip',
        Authorization: `Bearer ${token}`
      },
      body: JSON.stringify(newRequest)
    }).then(function (response) {
      return response.json();
    })
  );
  */
};

export const useNormalPlotData = (token: string) => {
  return useMutation({
    mutationFn: (newRequest) => {
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
  /*
      return useMutation('submitRoute', (newRequest) =>
    fetch(`${API_BASE_URL}/api/recommend_routes`, {
      method: 'post',
      headers: {
        'Content-Type': 'application/json',
        'Accept-Encoding': 'gzip',
        Authorization: `Bearer ${token}`
      },
      body: JSON.stringify(newRequest)
    }).then(function (response) {
      return response.json();
    })
  );
  */
};

export const useTaskPlotData = (taskId: string, token: string) => {
    /*
  return useQuery(
    ['getPlotData', taskId],
    async () => {
      const response = await fetch(`${API_BASE_URL}/api/recommend_routes_task/${taskId}`, {
        headers: {
          'Accept-Encoding': 'gzip',
          Authorization: `Bearer ${token}`
        }
      });
      const data = await response.json();
      // throw an error if status is started to trigger loading
      if (data?.status === 'started' || data?.status === 'pending') {
        throw new Error('Request initiated. Loading Results...');
      }
      return data;
    },
    {
      enabled: !!taskId,
      refetchOnWindowFocus: false,
      retry: true
    }
  );
  */

  return useQuery({
    queryKey: ['getPlotData'],
    queryFn: async (taskId) => {
        const response = await fetch(`${API_BASE_URL}/api/recommend_routes_task/${taskId}`, {
            headers: {
              'Accept-Encoding': 'gzip',
              Authorization: `Bearer ${token}`
            }
          });
          const data = await response.json();
          // throw an error if status is started to trigger loading
          if (data?.status === 'started' || data?.status === 'pending') {
            throw new Error('Request initiated. Loading Results...');
          }
          return data;
    },
    enabled: !!taskId,
    refetchOnWindowFocus: false,
    retry: true
  });
}
