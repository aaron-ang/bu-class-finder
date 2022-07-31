import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import Example from "./Example";
import { ReactQueryDevtools } from "@tanstack/react-query-devtools";
import { useEffect, useState } from "react";
import jwt_decode from "jwt-decode";

const App = () => {
  const queryClient = new QueryClient();
  const clientId = process.env.REACT_APP_CLIENT_ID as string;
  const [user, setUser] = useState({});

  const handleCredentialResponse = (res: any) => {
    console.log("Encoded JWT ID token: " + res.credential);
    const userObject: any = jwt_decode(res.credential);
    console.log(userObject);
    if (userObject.hd !== "bu.edu") {
      alert("Please sign in with a BU email");
      handleSignOut();
      return;
    }
    setUser(userObject);
    document.getElementById("signInDiv")!.hidden = true;
  };

  const handleSignOut = () => {
    // @ts-ignore
    google.accounts.id.disableAutoSelect();
    document.getElementById("signInDiv")!.hidden = false;
    setUser({});
  };

  useEffect(() => {
    /* global google */
    // @ts-ignore
    google.accounts.id.initialize({
      client_id: clientId,
      callback: handleCredentialResponse,
    });
    // @ts-ignore
    google.accounts.id.renderButton(document.getElementById("signInDiv"), {
      theme: "outline",
    });
    // @ts-ignore
    google.accounts.id.prompt();
  }, []);

  return (
    <QueryClientProvider client={queryClient}>
      <Example />
      <div id="signInDiv"></div>
      {Object.keys(user).length !== 0 && (
        <button onClick={handleSignOut}>Sign Out</button>
      )}
      <ReactQueryDevtools initialIsOpen={false} />
    </QueryClientProvider>
  );
};

export default App;
