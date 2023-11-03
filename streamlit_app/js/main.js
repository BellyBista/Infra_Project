const elements = window.parent.document.getElementsByTagName('footer');
const footerHTML = `
    <div style="display: flex; justify-content: space-between; align-items: center; padding: 10px;">
        <div>&copy; Powered by Iryss ${new Date().getFullYear()}</div>
        <div>In association with Omdena</div>
    </div>
`;
elements[0].innerHTML = footerHTML;