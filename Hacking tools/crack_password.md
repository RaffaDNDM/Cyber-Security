# John the Ripper
John the Ripper (also called simply ‘John’ ) is the most well known free password cracking tool that owes its success to its user-friendly command-line interface.
The main goal of the program is to discover the password that, if hashed, it is the same of the hashed stored one.
## Obtain the hashed stored passwords
They can be used by typing for example the following command on the Linux bash:
<pre lang="bash"><code>umask 077</code></pre>
<pre lang="bash"><code>unshadow /etc/passwd /etc/shadow > mypasswd</code></pre>

## Password cracking
After obtaining an hashed password and storing it in a file (e.g. mypasswd), you can crack it in several ways:
<pre lang="bash"><code>john mypasswd</code></pre>
You can also crack more than one password file simultaneously using the following commands:
<pre lang="bash"><code>john mypasswd1 mypasswd2</code></pre>
or
<pre lang="bash"><code>john *passwd* *.pwd</code></pre>

<details><summary>Show results</summary>
If you've got some passwords cracked, they are stored in $JOHN/john.pot. The john.pot file is not meant to be human-friendly and to display them in a readable format, you can type:
<pre lang="bash"><code>john --show mypasswd</td></code></pre>
There are other usefull options in addition to the previous ones:
<table>
  <tr>
    <td>--shells=-/etc/expired</td>
    <td>John ignores the disabled shell, called "/etc/expired".</td>
  </tr>
  <tr>
    <td>--shells=-expired</td>
    <td>John ignores (-) the disabled shell, called "/etc/expired" but also "/any/path/expired".</td>
  </tr>
  <tr>
    <td>--shells=-expired,newuser</td>
    <td>John ignores (-) "/any/path/expired" but also some other shells (e.g. "/etc/newuser/").</td>
  </tr>
  <tr>
    <td>--users=0</td>
    <td>Check if any root (UID 0) accounts got cracked.</td>
  </tr>
  <tr>
    <td>--users=0</td>
    <td>Check for cracked root (UID 0) accounts in multiple files.</td>
  </tr>
  <tr>
    <td>--users=root</td>
    <td>Check the root (username "root") account only.</td>
  </tr>
  <tr>
    <td>--groups=0,1</td>
    <td>Check for privileged groups.</td>
  </tr>
</table>
</details>

The main cracking modes, that John the Ripper can use, are:
1. Single cracking mode
2. Wordlist cracking mode
3. Incremental cracking mode

<details><summary>Single cracking mode</summary>
To manage the crack modes automatically, you can use the following commands:
<pre lang="bash"><code>john --single mypasswd</code></pre> or <pre lang="bash"><code>john -si mypasswd</code></pre>
You can also crack more than one password file in the same time:
<pre lang="bash"><code>john --single passwd1 passwd2</code></pre> or <pre lang="bash"><code>john --single *passwd* *.pwd</code></pre>
John will run faster and might even crack more passwords than it would if you ran it on each password file separately.
</details>
<details><summary>Wordlist cracking mode</summary>
The main option that John can use to execute this mode, are:
<table>
  <tr>
    <td>--wordlist=password.lst --rules</td>
    <td>Crack with tiny wordlist with word, applying mangling rules.</td>
  </tr>
  <tr>
    <td>-w=password.lst -ru</td>
    <td>Crack with tiny wordlist with word, applying mangling rules.</td>
  </tr> 
  <tr>
    <td>--wordlist=all.lst --rules</td>
    <td>Crack with a larger wordlist, also applying the mangling rule.</td>
  </tr>
  <tr>
    <td>john --wordlist=all.lst --rules mypasswd &</td>
    <td>Run John in background on <i>Linux</i>.</td>
  </tr>
  <tr>
    <td>john --session=allrules --wordlist=all.lst --rules mypasswd &</td>
    <td>Assign a session name.</td>
  </tr> 
</table>
You can also use other John utilities, for example: 
<pre lang="bash"><code>john --wordlist=all.lst --rules --stdout | unique mangled.lst</code></pre>
<pre lang="bash"><code>john --wordlist=mangled.lst mypasswd</code></pre>
to eliminate any duplicate candidate passwords.<br><br>
<pre lang="bash"><code>john --wordlist=all.lst --rules --stdout=8 | unique mangled8.lst</code></pre>
<pre lang="bash"><code>john --wordlist=mangled8.lst mypasswd</code></pre>
to optimize the cracking phase if you know that your target hash type truncates passwords at a given length.
</details>

<details><summary>Incremental cracking mode</summary>
<table>
  <tr>
    <td>john --incremental mypasswd</td>
    <td>Crack with incremental mode.</td>
  </tr>
  <tr>
    <td>john -i mypasswd</td>
    <td>Crack with incremental mode.</td>
  </tr>
  <tr>
    <td>john -i=digits mypasswd</td>
    <td>Try passwords of only digits from "0" to "99999999999999999999" (in an optimal order).</td>
  </tr>
</table>
</details>

There are also other useful commands that can be used to obtain information about the execution of John the Ripper.
<details><summary>Status of sessions</summary>
<table>
  <tr>
    <td>john --status</td>
    <td>View the status of the running session for the default one.</td>
  </tr>
  <tr>
    <td>john --status=allrules</td>
    <td>View the status of the running session for any other session.</td>
  </tr>
  <tr>
    <td>john --restore</td>
    <td>Continue interrupted default session.</td>
  </tr>
  <tr>
    <td>john --restore</td>
    <td>Continue any other interrupted.</td>
  </tr>
</table>
</details>

<details><summary>Specification of HASH type</summary>
You can specify the type of hash (e.g. MD5) used in the passwords by typing:
<pre lang="bash"><code>john --show --format=RAW-MD5 mypasswd</code></pre>
</details>

<details><summary>Other useful commands</summary>
<table>
  <tr>
    <td>john --list=formats</td>
    <td>Displays all the hash types supported.</td>
  </tr>
  <tr>
    <td>john --test</td>
    <td>Runs tests to displays the speed of cracking for various hash types.</td>
  </tr> 
  <tr>
    <td>john --help</td>
    <td>Displays all other options available for John.</td>
  </tr>
</table>
</details>
