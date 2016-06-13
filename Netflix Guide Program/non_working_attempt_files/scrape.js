/*Custom javascript to get movie titles on given page*/
var elements = document.getElementsByClassName("title-card-container");
	var i = 0;
	var nodes = [];
	var ids = [];
	var res = [];
	var info = [];
	var titles = [];
	for (i = 0; i < elements.length; i++)
	{
		nodes.push(elements.item(i));
	}
	for (i = 0; i < nodes.length; i++)
	{
		ids.push(__REACT_DEVTOOLS_GLOBAL_HOOK__.reactDevtoolsAgent.getIDForNode(nodes[i]));
	}
	for (i = 0; i < ids.length; i++)
	{
		res.push(__REACT_DEVTOOLS_GLOBAL_HOOK__.reactDevtoolsAgent.reactElements.get(ids[i]));
	}
	for (i = 0; i < res.length; i++)
	{
		info.push(res[i]._instance.getData());
	}
	for (i = 0; i < info.length; i++)
	{
		titles.push(info[i].title);
	}
	return titles;
	
	/*Alternative script, not working
	var elements = document.getElementsByClassName("title-card-container")
	var nodes = []
	for (i = 0; i < elements.length; i++)
	{
		nodes.push(elements.item(i));
	}
	var titles = nodes.map(t_callback);
	function t_callback(x)
	{
		(__REACT_DEVTOOLS_GLOBAL_HOOK__.reactDevtoolsAgent.reactElements.get(__REACT_DEVTOOLS_GLOBAL_HOOK__.reactDevtoolsAgent.getIDForNode(x)))._instance.getData().title;
	}*/