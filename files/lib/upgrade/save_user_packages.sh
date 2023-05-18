#!/bin/sh
# Save list of packages with the "user" flag to /etc/backup/user_packages.txt.

save_user_packages() {
	local files_list="$1"
	local user_packages="${ETCBACKUP_DIR}/user_packages.txt"

	[ "$SAVE_INSTALLED_PKGS" -eq 1 ] || return 0

	echo "$user_packages" >> "$files_list"

	[ "$CONF_BACKUP_LIST" -eq 1 ] && return 0

	mkdir -p "${user_packages%/*}"
	opkg status \
		| awk -v RS= '/Status: \S+ (\S+,)?user,?/{print $2}' \
		> "$user_packages"
}

sysupgrade_init_conffiles="$sysupgrade_init_conffiles save_user_packages"
