import React, { useContext, createContext, useEffect } from "react";
import {
  GoogleAuthProvider,
  signInWithPopup,
  // signInWithRedirect,
  signOut,
  onAuthStateChanged,
  User,
} from "firebase/auth";
import { auth } from "../firebase";

export interface Props {
  children: React.ReactNode;
}
interface Context {
  googleSignIn: () => void;
  logOut: () => void;
  user: User | null;
}

const AuthContext = createContext<Context | null>(null);

export const AuthContextProvider = ({ children }: Props) => {
  const [user, setUser] = React.useState<User | null>(null);

  const googleSignIn = () => {
    const provider = new GoogleAuthProvider();
    signInWithPopup(auth, provider);
  };

  const logOut = () => {
    signOut(auth);
  };

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (currentUser) => {
      setUser(currentUser);
    });
    return unsubscribe;
  }, []);

  return (
    <AuthContext.Provider value={{ googleSignIn, logOut, user }}>
      {children}
    </AuthContext.Provider>
  );
};

export const UserAuth = () => {
  return useContext(AuthContext);
};
