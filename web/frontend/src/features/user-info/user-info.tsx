import { useQuery } from '@tanstack/react-query';
import { useUserAuth } from '@/features/cognito/use-user-auth';

import { getDefaultAPI } from 'src/env';
import { UserProfile } from 'src/interface/api';

function UserInfo() {
  const { token } = useUserAuth();
  const api = getDefaultAPI(token);

  const { isPending, error, data } = useQuery({
    queryKey: ['getInfo'],
    queryFn: async () => {
      // const result = await defaultApi.getUserProfile();
      const result = await api.getUserProfile();
      return result.data as UserProfile;
    }
  });

  if (isPending) return 'Loading...';

  if (error) return 'An error has occurred: ' + error.message;

  return (
    <div>
      Dummy GET request to /api/user_profile
      <p>userid: {data.userid}</p>
      <p>username: {data.username}</p>
      <p>age: {data.age}</p>
    </div>
  );
}

export default UserInfo;
