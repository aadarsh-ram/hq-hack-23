import React from "react";
import ReactDOM from "react-dom";
import { ErrorBoundary } from "react-error-boundary";
import { ErrorFallback } from "./components";
import App from "./App";

ReactDOM.render(
	<ErrorBoundary FallbackComponent={ErrorFallback}>
		<App />
	</ErrorBoundary>,
	document.getElementById("root")
);
