import { Navigate } from "react-router-dom";
import { UserAuth } from "../context/AuthContext";
import { Props } from "../context/AuthContext";

const Protected = ({ children }: Props) => {
  const AuthContext = UserAuth();
  if (!AuthContext?.user) {
    return <Navigate to="/" />;
  }

  return <>{children}</>;
};

export default Protected;
