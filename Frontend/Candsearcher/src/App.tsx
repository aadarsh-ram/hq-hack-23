import React, { useState } from "react";
import AllRoutes from "./AllRoutes";
import Navbar from "./components/Navbar/Navbar";
import ResultsPage from "./components/ResultsPage/ResultsPage";
import Upload from "./components/Upload/Upload";
import styles from "./index.module.css";
import { HashRouter } from "react-router-dom";
import { Router } from "react-router-dom";
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
