// CUBE Exec View - Shared Navigation
// Add new pages here; all pages pick up the change automatically.

const PAGES = [
  { label: 'Consumer Projects', href: 'index.html',   icon: '📊' },
  { label: 'InfoSec Projects',        href: 'infosec.html', icon: '🔒' },
  { label: 'Infrastructure Projects', href: 'infra.html',   icon: '🏗️' },
  { label: 'Content Projects',        href: 'content.html',  icon: '📝' },
  { label: 'Corp Tech & WP Systems',  href: 'techops.html',       icon: '🖥️' },
  { label: 'Time Reporting',          href: 'timereporting.html', icon: '⏱️' },
];

(function renderNav() {
  const current = location.pathname.split('/').pop() || 'index.html';

  const tabs = PAGES.map(p => {
    const active = (current === p.href || (current === '' && p.href === 'index.html')) ? ' active' : '';
    return `<a class="topnav-tab${active}" href="${p.href}">${p.icon} ${p.label}</a>`;
  }).join('');

  const addBtn = `<a class="topnav-tab" href="#" onclick="alert('Share your next Jira view to add it here!')">+ Add View</a>`;

  document.getElementById('navTabs').innerHTML = tabs + addBtn;
})();
