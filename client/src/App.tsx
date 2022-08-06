import { Route, Routes } from "react-router-dom";
import Navbar from "./components/Navbar";
import Protected from "./components/Protected";
import { AuthContextProvider } from "./context/AuthContext";
import Account from "./pages/Account";
import Home from "./pages/Home";
import NotFound from "./pages/NotFound";

const App = () => {
  // const queryClient = new QueryClient();

  return (
    <AuthContextProvider>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route
          path="/account"
          element={
            <Protected>
              <Account />
            </Protected>
          }
        />
        <Route path="*" element={<NotFound />} />
      </Routes>
    </AuthContextProvider>
  );
};

export default App;
