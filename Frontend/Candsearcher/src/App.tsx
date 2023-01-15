import React, { useState } from "react";
import Upload from "./components/Upload/Upload";
import styles from "./index.module.css";

const App: () => JSX.Element = () => {

	return (
		<div className={styles.container}>
			<Upload />
		</div>
	);
};

export default App;
