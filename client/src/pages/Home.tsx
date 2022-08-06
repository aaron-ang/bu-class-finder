import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { UserAuth } from "../context/AuthContext";
import GoogleButton from 'react-google-button'

const Home = () => {
  const AuthContext = UserAuth();
  const navigate = useNavigate();

  const handleGoogleSignIn = async () => {
    try {
      await AuthContext?.googleSignIn();
    } catch (error) {
      console.log(error);
    }
  };

  useEffect(() => {
    if (AuthContext?.user != null) {
      navigate("/account");
    }
  }, [AuthContext?.user]);

  return (
    <div>
      <h1 className="text-center text-3xl font-bold py-8">Home Page</h1>
      <div className="max-w-[240px] m-auto py-4">
        <GoogleButton onClick={handleGoogleSignIn} />
      </div>
    </div>
  );
};

export default Home;
