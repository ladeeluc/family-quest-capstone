class NotificationWidget {
    constructor(element, CSRFToken) {
        this.element = element;
        this.notificationsElement = this.element.querySelector(".notifications");
        this.headerElement = this.element.querySelector("h5");
        this.badgeElement = this.element.querySelector(".notification-count");
        this.clearAllElement = this.element.querySelector(".notification-clear-all")
        this.notifications = [];
        this.CSRFToken = "";

        this.dismissNotification = this.dismissNotification.bind(this);
        this.dismissAllNotifications = this.dismissAllNotifications.bind(this);

        this.clearAllElement.addEventListener("click", this.dismissAllNotifications);

        this.getNotifications();
    }
    async getNotifications() {
        this.setLoading(true);
        let res = await fetch("/api/notifs/");
        if (res.ok) {
            this.CSRFToken = res.headers.get("X-CSRFToken");
            this.notifications = (await res.json()).notifs;
        }
        this.setLoading(false);
    }
    async dismissNotification(slug) {
        this.setLoading(true);
        let res = await fetch(`/api/notifs/${slug}/`, {
            method:"DELETE",
            headers: {
                "X-CSRFToken":this.CSRFToken
            }
        });
        if (res.ok) {
            this.CSRFToken = res.headers.get("X-CSRFToken");
            this.notifications = (await res.json()).notifs;
        }
        this.setLoading(false);
    }
    async dismissAllNotifications() {
        this.setLoading(true);
        let res = await fetch(`/api/notifs/`, {
            method:"DELETE",
            headers: {
                "X-CSRFToken":this.CSRFToken
            }
        });
        if (res.ok) {
            this.CSRFToken = res.headers.get("X-CSRFToken");
            this.notifications = (await res.json()).notifs;
        }
        this.setLoading(false);
    }
    setLoading(bool) {
        if (bool) {
            this.badgeElement.innerHTML = `<span role="status" aria-hidden="true" class="hidden spinner-border spinner-border-sm"></span>`; 
        } else {
            this.badgeElement.innerText = this.notifications.length;
            let navBadgeElement = document.querySelector("#nav-notifications-badge");
            if (this.notifications.length <= 0) {
                navBadgeElement.innerText = "";
            } else if (this.notifications.length < 100) {
                navBadgeElement.innerText = this.notifications.length;
            } else {
                navBadgeElement.innerText = "99+";
            }
            this.notificationsElement.innerHTML = "";
            let list = document.createElement("div");
            list.classList.add("list-group");
            for (let notif of this.notifications) {
                let elm = document.createElement("a");
                elm.href = notif.url;
                elm.classList.add("list-group-item", "list-group-item-action");
                let typeToStr = {
                    "comment":"commented on your post",
                    "message":"sent you a message"
                }
                let li = document.createElement("div");
                li.classList.add("d-flex", "w-100", "justify-content-between");
                let hdr = document.createElement("h5");
                hdr.classList.add("mb-1", "pe-3");
                hdr.innerHTML = `<span class="text-primary">${notif.from}</span> <span class="fw-normal">${typeToStr[notif.type]}<span>`;
                let closebtn = document.createElement("button");
                closebtn.classList.add("btn-close", "text-reset", "m-0");
                closebtn.addEventListener("click", (event) => {
                    event.preventDefault();
                    event.stopPropagation();
                    this.dismissNotification(notif.slug);
                });
                li.append(hdr, closebtn)
                let date = document.createElement("small");
                date.innerText = getDateString(new Date(notif.created_at));
                elm.append(li, date);
                list.append(elm);
            }
            this.notificationsElement.append(list);
        }
    }
}