import CustomLink from "./navbar";

export default function NavbarFinal() {
  return (
    <div className="absolute top-0 left-0 w-full h-16 flex items-center justify-center z-30">
      <nav className="flex items-center space-x-8">
        <CustomLink href="/home" label="Home" />
        <CustomLink href="/aboutus" label="About Us" />
        <CustomLink href="/instruments" label="Our Instruments" />
        <CustomLink href="/pricing" label="Pricing" />
      </nav>
    </div>
  );
}
