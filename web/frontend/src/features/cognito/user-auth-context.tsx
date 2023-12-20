import { createContext } from 'react';

type UserAuthProps = {
  token: string;
  userEmail: string;
  signOut: () => void;
};

export const UserAuthContext = createContext({} as UserAuthProps);
