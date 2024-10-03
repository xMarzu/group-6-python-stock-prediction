var dagcomponentfuncs = (window.dashAgGridComponentFunctions = window.dashAgGridComponentFunctions || {});

dagcomponentfuncs.StockLink = function (props) {
    return React.createElement(
        'a',
        {href: 'http://127.0.0.1:8050/stocks/' + props.value},
        props.value
    );
};
