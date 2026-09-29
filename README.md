# Khyar

Quick and dirty web scraper for the [chai and conversation](https://www.chaiandconversation.com/persian-dictionary?page=1#dictionary-results)  dictionary. This website does not have a search engine for the dictionary. So I cobbled together this tool so you can download and search it locally in a JSON file.
I use [jless](https://github.com/PaulJuliusMartinez/jless) for this


## HTML Dict structure
```html
<table class="table vocab-list" data-controller="vocab">
<thread></thread>
<thead></thead>
<tbody>
		<tr>
			<!-- phonetic -->
			<td></td> 
			<!-- english -->
			<td></td>
			<!-- script -->
			<td></td>
			<!-- appears_in -->
			<td></td>
		</tr>
		<tr>
			<td></td>
			<td></td>
			<td></td>
			<td></td>
		</tr>
		...
	</tbody>
</table>
```


## Dependencies
Made with the usual stack of python thingabobs
- [uv](https://docs.astral.sh/uv/getting-started/installation/#installation-methods) 
- [prek](https://prek.j178.dev/installation/) (dev)
- [ruff](https://docs.astral.sh/ruff/editors/setup/) (dev)
- [basedpyright](https://github.com/DetachHead/basedpyright) (dev)


## Running

Download all the html pages and store in its the default directory `html/`.
>```bash
>uv run main.py download --page-count 215
>```
> You should check what the page count is when you open it in your browser.

Parse all of the previously downloaded html files and write the result into `data.json`.
>```bash
>uv run main.py parse
>```



