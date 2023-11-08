import Container from "./Container";
import Logo from "./Logo";
import Search from "./Search";

const Navbar = () => {
  return (
    <div className="fixed w-full bg-[#FECCCB] z-10 shadow-xl">
      <div className="border-b-2 border-[#FECCCB]">
        <Container>
          <div className="flex flex-row items-center justify-around">
            <Search />
          </div>
        </Container>
      </div>
    </div>
  );
};

export default Navbar;
