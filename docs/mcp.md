# MCP Servers

* **Labels:** https://api.githubcopilot.com/mcp/x/labels
* **Issues:** https://api.githubcopilot.com/mcp/x/issues

## Content: mcp.json

```json
{
	"inputs": [],
	"servers": {
		"gh-labels": {
			"type": "http",
			"url": "https://api.githubcopilot.com/mcp/x/labels"
		},
		"gh-issues": {
			"type": "http",
			"url": "https://api.githubcopilot.com/mcp/x/issues"
		}
	},
}
```