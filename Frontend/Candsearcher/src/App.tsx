import React from "react";
import styles from "./index.module.css";
import AllRoutes from "./AllRoutes";
import Navbar from "./components/Navbar/Navbar";
import { BrowserRouter } from "react-router-dom";

const App: () => JSX.Element = () => {

	return (
		<BrowserRouter>
			<div className={styles.container}>
				<Navbar />
				<AllRoutes />		
			</div>
		</BrowserRouter>
	);
};

export default App;
