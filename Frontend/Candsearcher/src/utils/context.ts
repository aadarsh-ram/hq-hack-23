import { createContext } from "react";

interface PageContextType {
	page: "HOME" | "CONTENT" | "DESIGN" | "OC" | "";
	setPage: (page: "HOME" | "CONTENT" | "DESIGN" | "OC" | "") => void;
}

const PageContext = createContext<PageContextType>({
	page: "HOME",
	// eslint-disable-next-line @typescript-eslint/no-empty-function
	setPage: () => {},
});

export { PageContext };
