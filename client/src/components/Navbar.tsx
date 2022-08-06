import { UserAuth } from "../context/AuthContext";

const Navbar = () => {
  const AuthContext = UserAuth();

  const handleSignOut = async () => {
    try {
      await AuthContext?.logOut();
    } catch (error) {
      console.log(error);
    }
  };

  return (
    <div className="flex justify-between bg-gray-200 w-full p-4">
      <h1 className="text-center text-2xl font-bold">BU Class Finder</h1>
      {AuthContext?.user?.displayName ? (
        <button onClick={handleSignOut}>Logout</button>
      ) : null}
    </div>
  );
};

export default Navbar;
