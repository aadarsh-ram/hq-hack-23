interface TeamContent {
	pageKey: "HOME" | "CONTENT" | "DESIGN" | "OC";
	title: string;
	subtitle: string;
	description: string;
	backgroundURL: string;
	formURL: string;
	logoURL: string;
}

const teamContent: TeamContent[] = [
	{
		pageKey: "CONTENT",
		title: "Content",
		subtitle: "Voice",
		description:
			"Lorem ipsum dolor sit amet consectetur. Consequat malesuada imperdiet quis eget a dolor non. Commodo quisque varius elit congue massa in. Consectetur enim vitae sit.",
		backgroundURL: "/assets/images/bg-content.webp",
		formURL: "https://suhailahmed2627.vercel.app/",
		logoURL: "/assets/images/logo-content.webp",
	},
	{
		pageKey: "DESIGN",
		title: "Design",
		subtitle: "Face",
		description:
			"Lorem ipsum dolor sit amet consectetur. Consequat malesuada imperdiet quis eget a dolor non. Commodo quisque varius elit congue massa in. Consectetur enim vitae sit.",
		backgroundURL: "/assets/images/bg-design.webp",
		formURL: "https://suhailahmed2627.vercel.app/",
		logoURL: "/assets/images/logo-design.webp",
	},
	{
		pageKey: "OC",
		title: "Organizing Committee",
		subtitle: "Backbone",
		description:
			"Lorem ipsum dolor sit amet consectetur. Consequat malesuada imperdiet quis eget a dolor non. Commodo quisque varius elit congue massa in. Consectetur enim vitae sit.",
		backgroundURL: "/assets/images/bg-organizing.webp",
		formURL: "https://suhailahmed2627.vercel.app/",
		logoURL: "/assets/images/logo-organizing.webp",
	},
];

export { teamContent };
export type { TeamContent };
