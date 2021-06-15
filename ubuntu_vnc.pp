# https://linuxize.com/post/how-to-install-and-configure-vnc-on-ubuntu-20-04/

package {'tigervnc-standalone-server': ensure => installed}
#package {'tightvncserver': ensure => installed}
package {'xfce4': ensure => installed}
package {'xfce4-goodies': ensure => installed}

file {'vnc_passwd':
  ensure => present,
  path   => '/home/emanners/.vnc/passwd',
  mode   => '600',
  source => '/home/emanners/Documents/puppet_files/passwd',
}

file {'vnc_xstartup':
  ensure => present,
  path   => '/home/emanners/.vnc/xstartup',
  mode   => '700',
  source => '/home/emanners/Documents/puppet_files/xstartup',
}

file {'vnc_config':
  ensure => present,
  path   => '/home/emanners/.vnc/config',
  mode   => '700',
  source => '/home/emanners/Documents/puppet_files/config',
}

exec {'vncserver':
  path    => '/bin:/usr/bin',
  command => 'vncserver -localhost no',
  unless  => 'pgrep vncserver',
}
