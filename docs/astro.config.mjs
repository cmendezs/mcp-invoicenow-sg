import { defineConfig } from "astro/config";
import starlight from "@astrojs/starlight";
import starlightLlmsTxt from "starlight-llms-txt";

export default defineConfig({
  site: "https://cmendezs.github.io",
  base: "/mcp-invoicenow-sg/",
  integrations: [
    starlight({
      title: "mcp-invoicenow-sg",
      description: "MCP server for Singapore electronic invoicing (InvoiceNow)",
      customCss: ["./src/styles/docs-theme.css"],
      social: [
        { icon: "github", label: "GitHub", href: "https://github.com/cmendezs/mcp-invoicenow-sg" },
      ],
      sidebar: [
        { label: "Overview", link: "/" },
        { label: "Tools", link: "/tools/" },
        { label: "Changelog", link: "/changelog/" },
        { label: "Contributing", link: "/contributing/" },
        { label: "Security", link: "/security/" },
        { label: "Code of Conduct", link: "/code-of-conduct/" },
      ],
      plugins: [
        starlightLlmsTxt({
          projectName: "mcp-invoicenow-sg",
          description: "MCP server for Singapore electronic invoicing (InvoiceNow)",
          customSets: [
            {
              label: "Key links",
              description: "PyPI and MCP registry entries",
              links: ["https://pypi.org/project/mcp-invoicenow-sg/", "https://registry.modelcontextprotocol.io/v0/servers?search=io.github.cmendezs/mcp-invoicenow-sg"],
            },
          ],
        }),
      ],
    }),
  ],
});
