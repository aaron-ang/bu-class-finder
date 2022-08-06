import { UserAuth } from '../context/AuthContext';

const Account = () => {
    const AuthContext = UserAuth();

  return (
    <div className='w-[300px] m-auto'>
      <h1 className='text-center text-2xl font-bold pt-12'>Account</h1>
      <div>
        <p>Welcome, {AuthContext?.user?.displayName}</p>
      </div>
    </div>
  );
};

export default Account;